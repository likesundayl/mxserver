/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.lr;

/**
 * <tt>FactorLrScheduler.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午10:58:06
 * @version 1.0
 */
public class FactorLrScheduler extends LrScheduler {
	private int step = 10000;
	private float factor = 0.1f;
	private float stopFactorLr = 0.001f;
	
	public FactorLrScheduler(int step) {
		this.step = step > 0 ? step : -step;
		this.type = "Factor";
	}
	
	public FactorLrScheduler(int step, float factor, float stopFactorLr) {
		this.type = "Factor";
		this.step = step > 0 ? step : -step;
		this.factor = factor > 0 ? factor : -factor;
		this.stopFactorLr = stopFactorLr > 0 ? stopFactorLr : -stopFactorLr;
	}
}
