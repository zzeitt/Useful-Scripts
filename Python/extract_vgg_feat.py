import tensorflow as tf
import numpy as np


MODEL_PATH = '../Assests/my_model.pb'

g_mine = tf.Graph()
with g_mine.as_default():
    with tf.gfile.FastGFile(MODEL_PATH, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

def get_inception_feat(s_image):
    with tf.Session(graph=g_mine) as sess:
        # Preprocess the image
        fname = s_image
        raw_img = tf.io.gfile.GFile(fname, 'rb').read()
        tf_img = tf.image.decode_jpeg(raw_img).eval()
        tf_fl_img = tf.cast(tf_img, dtype=tf.float32).eval()
        if tf_fl_img.shape[2] == 1:
            tf_fl_img = np.repeat(tf_fl_img, 3, axis=2)
        tf_fl_img_rsz2 = tf.image.resize(
            tf_fl_img, [299, 299], 'bilinear').eval()
        tf_fl_img_rsz2_expand = np.expand_dims(tf_fl_img_rsz2, 0)
        tf_input = tf.subtract(tf_fl_img_rsz2_expand,
                               tf.constant([128], dtype=tf.float32)).eval()
        tf_input = tf.multiply(tf_input, tf.constant(
            [0.0078125], dtype=tf.float32)).eval()

        x_pool_3 = sess.graph.get_tensor_by_name('pool_3/AvgPool:0')
        x_softmax = sess.graph.get_tensor_by_name('softmax/truediv:0')
        pred = sess.run(x_pool_3, {'input_1:0': tf_input}).squeeze()
        return pred


if __name__ == '__main__':
    s_image = (
        '/home/zeit/SDB/NiseEngFolder/newFile/forWork/forCooperation/'
        'forOCR/train_gender/allset/601155.jpg')
    
    feat = get_inception_feat(s_image)
    print(f'====> feat: {feat}')
