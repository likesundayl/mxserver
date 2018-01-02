/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.opt;

/**
 * <tt>Optimizer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午9:36:22
 * @version 1.0
 */
public abstract class Optimizer {
	protected String type;
	protected float baseLr = 0.01f;
	protected float weightDecay = 0f;
	
	public Optimizer(float baseLr, float weightDecay) {
		this.baseLr = baseLr > 0 ? baseLr : -baseLr;
		this.weightDecay = weightDecay > 0 ? weightDecay : -weightDecay;
	}
	
	public abstract String toJSON();
}
