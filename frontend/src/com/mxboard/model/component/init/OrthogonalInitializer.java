/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.init;

/**
 * <tt>OrthogonalInitializer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午11:10:07
 * @version 1.0
 */
public class OrthogonalInitializer extends Initializer {
	private float scale = 1.414f;
	private String randType = "uniform";
	
	public OrthogonalInitializer() {
		this.type = "Orthogonal";
	}
	
	public OrthogonalInitializer(float scale, String randType) {
		this.scale = scale > 0 ? scale : -scale;
		this.randType = randType;
	}

	@Override
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"type\": \"")
				.append(type).append("\", \"init_config\": {")
				.append("\"scale\": \"")
				.append(scale).append("\", \"rand_type\": \"")
				.append(randType).append("\"}}");
		
		return builder.toString();
	}
}
