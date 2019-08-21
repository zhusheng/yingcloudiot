import numpy as np
import os
import sys
import tarfile
import tensorflow as tf
import zipfile
from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import time

sys.path.append('..')
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from yingcloudiot.settings import detection_graph, PATH_TO_FROZEN_GRAPH, PATH_TO_LABELS

if StrictVersion(tf.__version__) < StrictVersion('1.12.0'):
      raise ImportError('Please upgrade your TensorFlow installation to v1.12.*.')


def init_graph():
    '''
    初始化图
    '''
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        # 获取一个文件操作句柄，加载模型文件
        with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid: 
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

def load_image_into_numpy_array(image):
    '''
    把图片加载为二进制
    '''
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

def run_inference_for_single_image(image, graph):
    '''
    预测单张图片
    '''
    with graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in ['num_detections', 'detection_boxes', 'detection_scores','detection_classes', 'detection_masks']: 
                tensor_name = key + ':0' 
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
                if 'detection_masks' in tensor_dict:
                    # The following processing is only for single image
                    detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                    detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                    # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                    real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, detection_boxes, image.shape[1], image.shape[2])
                    detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    # Follow the convention by adding back the batch dimension
                    tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            # Run inference
            output_dict = sess.run(tensor_dict,feed_dict={image_tensor: image})

            # all outputs are float32 numpy arrays, so convert types as appropriate
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.int64)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]
            return output_dict

def files_path(path):
    """
    遍历某个路径下的图片，返回图片的路径集合
    """
    items = os.listdir(path)
    newlist = []
    for item in items:
        if item.endswith(".jpg") or item.endswith(".png"):
            newlist.append(os.path.join(path, item))
    print(newlist)
    return newlist

def detection_with_single(path):
    """
    预测单张图片
    """
    # 初始化图
    init_graph()
    # 加载标签映射关系文件
    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
    # 标记后的图片尺寸
    IMAGE_SIZE = (12, 8)
    image = Image.open(path)
    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    image_np = load_image_into_numpy_array(image)
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    # Actual detection.
    # 调用预测函数
    output_dict = run_inference_for_single_image(image_np_expanded, detection_graph)
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            instance_masks=output_dict.get('detection_masks'),
            use_normalized_coordinates=True,
            line_thickness=8)
    plt.figure(figsize=IMAGE_SIZE)
    plt.imshow(image_np)

    file_path, file_name = os.path.split(str(path))
    filea, fileb = os.path.splitext(file_name)
    # 返回时间格式：2019-08-19-11-37-52
    current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    output_path ='upload/recognition_result/' + filea+ '-' + current_time + fileb
    print(output_path)
    plt.savefig(output_path)
    plt.show()

    dict1 = {}
    list1 = []
    
    # 获取预测结果：预测类别和概率
    list_len = len(output_dict['detection_scores'])
    # 输出结果中概率大于90%的所有预测结果
    for i in range(list_len):
        if output_dict['detection_scores'][i] > 0.9:
            # 类别索引
            index = output_dict['detection_classes'][i]
            # 预测类别
            type_name = category_index[index]['name']
            # 概率
            type_probability = output_dict['detection_scores'][i]

            list1.append('{type: %s, probability: %s}' %(type_name,type_probability))

   
    dict1['result_url'] = output_path
    dict1['recognition_time'] = time.time()
    return dict1, list1

def detection(path_dir):
    """
    识别图片集
    """
    paths = files_path(path_dir)
    for image_path in paths:
        detection_with_single(image_path)
        

if __name__ == '__main__':
    path1 = '../object_detection/test_images'
    path2 = '/Users/zhusheng/WorkSpace/Dataset/15-object_detection/image1'

    #detection(path1)
    detection_with_single('/Users/zhusheng/WorkSpace/Dataset/15-object_detection/image1/image4.jpg')
    