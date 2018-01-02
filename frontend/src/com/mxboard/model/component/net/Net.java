/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.net;

/**
 * <tt>Net.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午9:36:57
 * @version 1.0
 */
public class Net {
	private String name;
	private int numClasses;
	private String dtype = "float32";
	private NetConfig netConfig;
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"name\": \"")
				.append(name).append("\", \"num_classes\": \"")
				.append(numClasses).append("\", \"dtype\": \"")
				.append(dtype).append("\", \"net_config\": ")
				.append(netConfig.toJSON());
		
		builder.append("}");
		return builder.toString();
	}
}
