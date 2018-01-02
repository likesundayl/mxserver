/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component;

/**
 * <tt>CheckPointParam.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 下午3:44:34
 * @version 1.0
 */
public class CheckPointParam {
	private String prefix;
	private int epoch;
	
	public CheckPointParam(String prefix, int epoch) {
		this.prefix = prefix;
		this.epoch = epoch > 0 ? epoch : -epoch;
	}
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");		
		builder.append("\"prefix\": \"")
				.append(prefix).append("\", \"epoch\": \"")
				.append(epoch).append("\"}}");
		
		return builder.toString();
	}
}
