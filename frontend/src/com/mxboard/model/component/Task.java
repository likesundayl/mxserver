/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component;

import com.mxboard.model.component.net.Symbol;

/**
 * <tt>Task.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午9:52:53
 * @version 1.0
 */
public class Task {
	private int id;
	private boolean forTraining = true;
	private Symbol net;
	private TrainParam trainParam;
	private TestParam testParam;
}
