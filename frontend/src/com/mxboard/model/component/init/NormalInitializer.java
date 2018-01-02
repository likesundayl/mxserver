/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.init;

/**
 * <tt>NormalInitializer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午11:09:17
 * @version 1.0
 */
public class NormalInitializer extends Initializer {
	private float sigma = 0.01f;
	
	public NormalInitializer() {
		this.type = "Normal";
	}
	
	public NormalInitializer(float sigma) {
		this.sigma = sigma > 0 ? sigma : -sigma;
	}

	@Override
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"type\": \"")
				.append(type).append("\", \"init_config\": {")
				.append("\"sigma\": \"")
				.append(sigma).append("\"}}");
		
		return builder.toString();
	}
}
