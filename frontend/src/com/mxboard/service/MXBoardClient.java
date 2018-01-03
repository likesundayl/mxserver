/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.service;

import java.util.HashMap;

import com.mxboard.model.component.Task;
import com.mxboard.service.rpc.MXNetServiceGrpc;
import com.mxboard.service.rpc.MXNetServiceGrpc.MXNetServiceBlockingStub;
import com.mxboard.service.rpc.Mxboard.TaskId;
import com.mxboard.service.rpc.Mxboard.TaskParameter;
import com.mxboard.service.rpc.Mxboard.TaskState;
import com.mxboard.util.XMLConfigParser;

import io.grpc.Channel;
import io.grpc.ManagedChannelBuilder;

/**
 * <tt>MXBoardClient.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2017年12月24日 下午10:42:21
 * @version 1.0
 */
public class MXBoardClient {
	private static HashMap<String, String> grpcConfig = (new XMLConfigParser()).getGRpcConfig();
	private Channel channel;
	private MXNetServiceBlockingStub stub;
	
	public MXBoardClient() {
		channel = ManagedChannelBuilder.forAddress(grpcConfig.get("host"), Integer.valueOf(grpcConfig.get("port"))).usePlaintext(true).build();
		stub = MXNetServiceGrpc.newBlockingStub(channel);
	}
	
	public TaskState startTask(Task task) {
		TaskParameter taskParameter = TaskParameter.newBuilder().setId(TaskId.newBuilder().setTaskId(task.taskId()).build()).setTaskDesc(task.toJSON()).build();
		return stub.startTask(taskParameter);
	}
	
	public TaskState stopTask(String taskId) {
		TaskId id = TaskId.newBuilder().setTaskId(taskId).build();
		return stub.stopTask(id);
	}
}
