/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.opt;

/**
 * <tt>RMSPropOptimizer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午11:14:39
 * @version 1.0
 */
public class RMSPropOptimizer extends Optimizer {
	private float gamma1 = 0.9f;
	private float gamma2 = 0.9f;
	private float epsilon = 1e-8f;
	private boolean centered = false;

	public RMSPropOptimizer(float baseLr, float weightDecay, float gamma1, float gamma2, float epsilon, boolean centered) {
		super(baseLr, weightDecay);
		this.type = "rmsprop";
		this.gamma1 = gamma1 > 0 ? gamma1 : -gamma1;
		this.gamma2 = gamma2 > 0 ? gamma2 : -gamma2;
		this.epsilon = epsilon > 0 ? epsilon : -epsilon;
		this.centered = centered;
	}

	@Override
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"type\": \"")
				.append(type).append("\", \"opt_config\": {")
				.append("\"base_lr\": \"")
				.append(baseLr).append("\", \"wd\": \"")
				.append(weightDecay).append("\", \"gamma1\": \"")
				.append(gamma1).append("\", \"gamma2\": \"")
				.append(gamma2).append("\", \"epsilon\": \"")
				.append(epsilon).append("\", \"centered\": \"")
				.append(centered).append("\"}}");
		
		return builder.toString();
	}

}
