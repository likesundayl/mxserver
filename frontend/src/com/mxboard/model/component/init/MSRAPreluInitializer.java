/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.init;

/**
 * <tt>MSRAPreluInitializer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午11:11:03
 * @version 1.0
 */
public class MSRAPreluInitializer extends Initializer {
	private float slope = 0.25f;
	private String factorType = "avg";
	@Override
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"type\": \"")
				.append(type).append("\", \"init_config\": {")
				.append("\"slope\": \"")
				.append(slope).append("\", \"factor_type\": \"")
				.append(factorType).append("\"}}");
		
		return builder.toString();
	}
}
