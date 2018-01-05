/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.opt;

/**
 * <tt>SGDOptimizer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午11:12:11
 * @version 1.0
 */
public class SGDOptimizer extends Optimizer {
	private float momentum = 0.9f;
	
	public SGDOptimizer() {
		super(0.01f, 0.0005f);
		this.type = "sgd";
		this.momentum = 0.9f;
	}
	
	public SGDOptimizer(float baseLr, float momentum, float weightDecay) {
		super(baseLr, weightDecay);
		this.type = "sgd";
		this.momentum = momentum;
	}

	@Override
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"type\": \"")
				.append(type).append("\", \"opt_config\": {")
				.append("\"base_lr\": \"")
				.append(baseLr).append("\", \"wd\": \"")
				.append(weightDecay).append("\", \"momentum\": \"")
				.append(momentum).append("\"}}");
		
		return builder.toString();
	}
}
