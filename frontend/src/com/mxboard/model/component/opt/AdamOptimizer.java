/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.opt;

/**
 * <tt>AdamOptimizer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午11:12:52
 * @version 1.0
 */
public class AdamOptimizer extends Optimizer {
	private float beta1 = 0.9f;
	private float beta2 = 0.999f;
	private float epsilon = 1e-8f;
	
	public AdamOptimizer(float baseLr, float weightDecay, float beta1, float beta2, float epsilon) {
		super(baseLr, weightDecay);
		this.type = "adam";
		this.beta1 = beta1 > 0 ? beta1 : -beta1;
		this.beta2 = beta2 > 0 ? beta2 : -beta2;
		this.epsilon = epsilon > 0 ? epsilon : -epsilon;
	}
	
	@Override
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"type\": \"")
				.append(type).append("\", \"opt_config\": {")
				.append("\"base_lr\": \"")
				.append(baseLr).append("\", \"wd\": \"")
				.append(weightDecay).append("\", \"beta1\": \"")
				.append(beta1).append("\", \"beta2\": \"")
				.append(beta2).append("\", \"epsilon\": \"")
				.append(epsilon).append("\"}}");
		
		return builder.toString();
	}
}
