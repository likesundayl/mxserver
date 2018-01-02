/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component;

import com.mxboard.model.component.init.Initializer;
import com.mxboard.model.component.lr.LrScheduler;
import com.mxboard.model.component.net.Net;
//import com.mxboard.model.component.net.Symbol;
import com.mxboard.model.component.opt.Optimizer;

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
	private Net net;
//	private Symbol symbol;
	private Data data;
	private Label label;
	private Initializer initializer;
	private Optimizer optimizer;
	private LrScheduler lrScheduler;
	
}
