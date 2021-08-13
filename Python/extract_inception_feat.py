import tensorflow as tf
import numpy as np
from tqdm import tqdm
import os

# =====================================================
# Load Model
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
MODEL_PATH = '../Assests/inception.pb'

g_mine = tf.Graph()
with g_mine.as_default():
    with tf.gfile.FastGFile(MODEL_PATH, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
    
# =====================================================
# Functions
def getFilePaths(path):
    # read a folder, return the complete path
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    ret.sort()
    return ret

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
    # Saving
    li_imgs = getFilePaths(
        '/home/zeit/SDB/NiseEngFolder/newFile/forWork/forCooperation/'
        'forOCR/train_gender/allset')
    dict_feats = {}
    s_save = '/home/zeit/SDB/NiseEngFolder/newFile/forWork/forCooperation/forOCR/train_gender/'
    n_save = 'allset_feats'
    
    for idx, s_in in enumerate(tqdm(li_imgs)):
        # if idx > 2: break
        n_img = os.path.basename(s_in)[:-4]
        feat = get_inception_feat(s_in)
        dict_feats[n_img] = feat
        
    np.savez(f'{s_save}{n_save}', dict_feats)
    
    # Loading
    npzfile = np.load(f'{s_save}{n_save}.npz', allow_pickle=True)
    print(f'====> npzfile: \n{npzfile["arr_0"].item()}')

