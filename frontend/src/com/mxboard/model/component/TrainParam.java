/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component;

import com.mxboard.model.component.init.Initializer;
import com.mxboard.model.component.init.NormalInitializer;
import com.mxboard.model.component.lr.FactorLrScheduler;
import com.mxboard.model.component.lr.LrScheduler;
import com.mxboard.model.component.opt.Optimizer;
import com.mxboard.model.component.opt.SGDOptimizer;

/**
 * <tt>TrainParam.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 下午3:42:52
 * @version 1.0
 */
public class TrainParam {
	private int numEpoch = 250;
	private String kvStore = "local";
	private LabelParam labelParam = new LabelParam();
	private LrScheduler lrScheduler = new FactorLrScheduler(10000);
	private Optimizer optimizer = new SGDOptimizer();
	private Initializer initializer = new NormalInitializer();
	private DataParam dataParam;
	private String savePrefix;
	private int savePeriod;
	
	public TrainParam(DataParam dataParam, LabelParam labelParam, int numEpoch, String kvStore, LrScheduler lrScheduler, Optimizer optimizer, Initializer initializer, String savePrefix, int savePeriod) {
		this.dataParam = dataParam;
		this.labelParam = labelParam;
		this.numEpoch = numEpoch > 0 ? numEpoch : -numEpoch;
		this.kvStore = kvStore;
		this.lrScheduler = lrScheduler;
		this.initializer = initializer;
		this.optimizer = optimizer;
		this.savePrefix = savePrefix;
		this.savePeriod = savePeriod > 0 ? savePeriod : -savePeriod;
	}
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"num_epoch\": \"")
				.append(numEpoch).append("\", \"kvstore\": \"")
				.append(kvStore).append("\", \"save_prefix\": \"")
				.append(savePrefix).append("\", \"save_period\": \"")
				.append(savePeriod).append("\", \"data_param\": ")
				.append(dataParam.toJSON()).append(", \"label_param\": ")
				.append(labelParam.toJSON()).append(", \"lr_scheduler\": ")
				.append(lrScheduler.toJSON()).append(", \"optimizer\": ")
				.append(optimizer.toJSON()).append(", \"initializer\": ")
				.append(initializer.toJSON()).append("}");
		
		return builder.toString();
	}
}
