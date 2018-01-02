/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.init;

/**
 * <tt>UniformInitializer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午11:09:04
 * @version 1.0
 */
public class UniformInitializer extends Initializer {
	private float scale = 0.07f;
	
	public UniformInitializer() {
		this.type = "Uniform";
	}
	
	public UniformInitializer(float scale) {
		this.type = "Uniform";
		this.scale = scale > 0 ? scale : -scale;
	}
}
