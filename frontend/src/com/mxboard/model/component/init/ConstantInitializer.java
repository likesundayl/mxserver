/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.init;

/**
 * <tt>ConstantInitializer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午11:08:49
 * @version 1.0
 */
public class ConstantInitializer extends Initializer {
	private float constValue = 1;
	
	public ConstantInitializer(float constValue) {
		this.type = "Constant";
		this.constValue = constValue;
	}
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"type\": \"")
				.append(type).append("\", \"init_config\": {")
				.append("\"const_value\": \"")
				.append(constValue).append("\"}}");
		
		return builder.toString();
	}
	
	public static void main(String[] args) {
		Initializer initializer = new ConstantInitializer(2.5f);
		System.out.println(initializer.toJSON());
	}
}
