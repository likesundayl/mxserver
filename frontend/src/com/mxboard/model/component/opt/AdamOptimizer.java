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
}
