/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.opt;

/**
 * <tt>AdaGradOptimizer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午11:14:16
 * @version 1.0
 */
public class AdaGradOptimizer extends Optimizer {
	private float eps = 1e-7f;
	
	public AdaGradOptimizer(float baseLr, float weightDecay, float eps) {
		super(baseLr, weightDecay);
		this.type = "agagrad";
		this.eps = eps > 0 ? eps : -eps;
	}
	
	@Override
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"type\": \"")
				.append(type).append("\", \"opt_config\": {")
				.append("\"base_lr\": \"")
				.append(baseLr).append("\", \"weight_decay\": \"")
				.append(weightDecay).append("\", \"eps\": \"")
				.append(eps).append("\"}}");
		
		return builder.toString();
	}
}
