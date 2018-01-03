/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component;

/**
 * <tt>Label.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午9:53:40
 * @version 1.0
 */
public class LabelParam {
	private String name = "softmax_label";
	private int[] shapes = {1};
	
	public LabelParam() {
		
	}
	
	public LabelParam(String name) {
		this.name = name;
	}
	
	public LabelParam(String name, int...shapes) {
		this.name = name;
		if (shapes.length == 0) {
			shapes = new int[] {1};
		} else {
			for(int shape : shapes) {
				if(shape == 0) {
					shape = 1;
				}
				shape = shape > 0 ? shape : -shape;
			}
			this.shapes = shapes;
		}
	}
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"name\": \"")
				.append(name).append("\", \"shapes\": [");
		for (int i = 0 ; i < shapes.length ; i++) {
			builder.append("\"").append(shapes[i]).append("\"");
			if (i != shapes.length - 1) {
				builder.append(", ");
			}
		}
		builder.append("]}");
		
		return builder.toString();
	}
}
