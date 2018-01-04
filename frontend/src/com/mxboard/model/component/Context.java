/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component;

import java.util.ArrayList;

/**
 * <tt>Context.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月4日 下午2:06:48
 * @version 1.0
 */
public class Context {
	private String deviceName = "gpu";
	private ArrayList<Integer> deviceIds = new ArrayList<>();
	
	public Context() {
		deviceIds.add(0);
	}
	
	public Context(boolean isGPU, int...deviceIds) {
		if (isGPU) {
			if (deviceIds.length == 0) {
				this.deviceIds.add(0);
			} else {
				for (int id : deviceIds) {
					this.deviceIds.add(id >= 0 ? id : -id);
				}
			}
		} else {
			deviceName = "cpu";
			this.deviceIds.add(0);
		}
	}
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("[");
		
		int index = 0;
		int totalDeviceNum = deviceIds.size();
		for (Integer deviceId : deviceIds) {
			builder.append("{\"device_name\": \"")
					.append(deviceName).append("\", \"device_id\": \"")
					.append(deviceId).append("\"}");
			if (index != totalDeviceNum - 1) {
				builder.append(", ");
			}
			index++;
		}
		builder.append("]");
		
		return builder.toString();
	}
}
