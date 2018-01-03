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
	private String id;
	private boolean forTraining = true;
	private Symbol net;
	private TrainParam trainParam;
	private TestParam testParam;
	
	public Task(String id, boolean forTraining, Symbol net, TrainParam trainParam, TestParam testParam) {
		this.id = id;
		this.forTraining = forTraining;
		this.net = net;
		this.trainParam = trainParam;
		this.testParam = testParam;
	}
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"task_id\": \"")
				.append(id).append("\", \"for_training\": \"")
				.append(forTraining).append("\", \"net\": ")
				.append(net.toJSON()).append(", ");
		if(forTraining) {
			builder.append("\"train_param\": ").append(trainParam.toJSON()).append("}");
		} else {
			builder.append("\"test_param\": ").append(testParam.toJSON()).append("}");
		}
		
		return builder.toString();
	}
}
