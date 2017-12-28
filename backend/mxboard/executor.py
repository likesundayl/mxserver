# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from mxnet.module import Module


class Executor(Module):
    def __init__(self, symbol, data_iters, ctx_list, initializer, lr_scheduler, optimizer, data_names, label_names):
        super(Executor, self).__init__(symbol=symbol, data_names=data_names, label_names=label_names, logger=None,
                                       context=ctx_list, work_load_list=None, fixed_param_names=None, state_names=None)
        self._train_iter = data_iters[0]
        if len(data_iters) == 2:
            self._val_iter = data_iters[1]
        else:
            self._val_iter = None

    def execute(self):
        # TODO:
        pass
