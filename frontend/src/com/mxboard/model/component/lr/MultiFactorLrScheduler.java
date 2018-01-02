/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.lr;

import java.util.Arrays;

/**
 * <tt>MultiFactorLrScheduler.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午10:59:00
 * @version 1.0
 */
public class MultiFactorLrScheduler extends LrScheduler {
	private int[] steps;
	private float factor = 0.1f;
	
	public MultiFactorLrScheduler(int...steps) {
		this.type = "MultiFactor";
		initSteps(steps);
	}
	
	public MultiFactorLrScheduler(float factor, int...steps) {
		this.type = "MultiFactor";
		this.factor = factor > 0 ? factor : -factor;
		initSteps(steps);
	}
	
	private void initSteps(int...steps) {
		if(steps.length == 0) {
			this.steps = new int[]{10000};
		} else {
			for(int step : steps) {
				step =  step > 0 ? step : -step;
			}
			Arrays.sort(steps);
			this.steps = steps;
		}
	}
}
