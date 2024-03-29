# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 26/02/18 上午 11:37
from config import FLASK_PORT

TEST_BASE_URL = 'http://127.0.0.1:%s' % FLASK_PORT
TRAIN_TEST_URL = TEST_BASE_URL + '/train'
EVALUATE_TEST_URL = TEST_BASE_URL + '/test'
INFERENCE_TEST_URL = TEST_BASE_URL + '/inference'
STOP_TEST_URL = TEST_BASE_URL + '/stop'
QUERY_GPU_TEST_URL = TEST_BASE_URL + '/gpu'

TRAIN_REQUEST_JSON = {
    "classes": {"0": "airplane", "1": "automobile", "2": "bird", "3": "cat", "4": "deer", "5": "dog", "6": "frog",
                "7": "horse", "8": "ship", "9": "truck"},
    "net": {
        "type": "built_in",
        "name": "alexnet",
        "config": {
            "num_classes": "10"
        }
    },
    "for_training": "0",
    "target": "classify",
    "context": [
        {"device_name": "gpu", "device_id": "0"}
    ],
    "eval_metrics": ["acc"],
    "train_param": {
        "begin_epoch": "0",
        "num_epoch": "250",
        "kvstore": "local",
        "save_prefix": "alex",
        "save_period": "50",
        "resume_config": {
            # 0 for True, 1 for False
            "is_resume": "1",
            "ckp": {}
        },
        "data_param": {
            # "local" or "internet"
            "source": "local",
            # "rec" or "raw"
            "ftype": "rec",
            "batch_size": "32",
            "shuffle": "0",
            "name": "data",
            "shapes": ["3", "128", "128"],
            "file_url": {
                # If ftype is raw
                # "train_img_path": "",
                # "train_lst_path": "",
                # "val_img_path": "",
                # "val_lst_path": "",

                # if ftype if rec
                "train_rec": "train.rec",
                "train_idx": "train.idx",
                "val_rec": "val.rec",
            }
        },
        "label_param": {
            "name": "softmax_label",
            "shapes": ["1"]
        },
        "lr_scheduler": {
            "type": "Factor",
            "lr_scheduler_config": {
                "step": "1000",
                "factor": "0.1",
                "stop_factor_lr": "0.001"
            }
        },
        "optimizer": {
            "type": "sgd",
            "opt_config": {
                "base_lr": "0.1",
                "wd": "0.0005",
                "momentum": "0.9"
            }
        },
        "initializer": {
            "type": "normal",
            "init_config": {
                "sigma": "0.25"
            }
        }
    },
    "test_param": {}
}

TEST_REQUEST_JSON = {
    "classes": {"0": "airplane", "1": "automobile", "2": "bird", "3": "cat", "4": "deer", "5": "dog", "6": "frog",
                "7": "horse", "8": "ship", "9": "truck"},
    "net": {
        "type": "built_in",
        "name": "alexnet",
        "config": {
            "num_classes": "10"
        }
    },
    # 0 for True, 1 for false
    "for_training": "1",
    "target": "classify",
    "context": [
        {"device_name": "gpu", "device_id": "0"}
    ],
    "eval_metrics": ["acc"],
    "train_param": {},
    "test_param": {
        "ckp": {
            "prefix": "alexnet",
            "epoch": "50"
        },
        "test_img_config": {
            # "local" or "internet"
            "source": "local",
            # 0 for True(correct labels are provided), 1 for False(correct labels are not provided)
            "use_label": "1",
            "label": {
                "cls_label": "test.txt",
                "detec_xml_label": "annotations.txt"
            },
            "img_list": ["xxx.jpg", "yyy.jpg", "zzz.jpg"],
            "img_shapes": ["128", "128"]
        }
    }
}

INFERENCE_REQUEST_JSON = {
    "deploy_id": "",
    "batch_size": "1",
    "top_k": "1",
    "context": [
        {"device_name": "gpu", "device_id": "0"}
    ],
    "urls": [
        "a.png",
        "b.png"
    ]
}

STOP_REQUEST_JSON = {
    "task_id": "19700101"
}

DEPLOY_REQUEST_JSON = {
    "target": "",
    "classes": {},
    "net": {
        "type": "built_in",
        "name": "alexnet",
        "config": {
            "num_classes": "10"
        }
    },
    "ckp": {
        "prefix": "",
        "epoch": ""
    }
}
