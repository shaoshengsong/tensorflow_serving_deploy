使用 TensorFlow Serving 部署模型

以 faster_rcnn_resnet101_coco_2018_01_28 为利 说明如何部署

[TensorFlow models 下载地址](https://github.com/tensorflow/models)


TensorFlow models的Object Detection目录
 

    models/research/object_detection/g3doc/detection_model_zoo.md 

先从[Tensorflow detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) 下载faster_rcnn_resnet101_coco_2018_01_28 ，如果链接失效 直接在搜索引擎里搜索关键字 Tensorflow detection model zoo


需要更改目录中一个文件夹的名字

原始


     |     |--faster_rcnn_resnet101_coco_2018_01_28/
     |             |
     |             |--saved_model/
     |             |   |
     |             |   |-saved_model.pb    
     |             |   |
     |             |   |-variables/
     |             |
     |             |--checkpoint

更改之后,其他的可以删除

     |     |--faster_rcnn_resnet101_coco_2018_01_28/
     |             |
     |             |--00001/
     |                |
     |                |-saved_model.pb 
     |                |
     |                |-variables/




   把faster_rcnn_resnet101_coco_2018_01_28文件夹 放到data文件夹中




   假设我们当前的工作目录是tensorflow_serving_deploy

 执行main.py 需要Object detection 文件夹的文件,路径是models/research/object_detection
拷贝到tensorflow_serving_deploy文件夹中
    
    运行命令

    docker run -t --rm -p 8501:8501 \
       -v "$(pwd)/data/faster_rcnn_resnet101_coco_2018_01_28:/models/faster_rcnn_resnet" \
       -e MODEL_NAME=faster_rcnn_resnet \
       tensorflow/serving &

**执行python main.py 的结果**

         * Serving Flask app "app" (lazy loading)
     * Environment: production
       WARNING: Do not use the development server in a production environment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

   
   **在浏览器中打开**
   http://127.0.0.1:5000/
   
上传的文件会在upload文件夹

 main.py 代码更改自 object_detection_tutorial.ipynb

data中的labels.pbtxt是拷贝自
tensorflow/models/research/object_detection/data/mscoco_label_map.pbtxt 
只是名字改了
