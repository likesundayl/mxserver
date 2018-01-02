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
}
