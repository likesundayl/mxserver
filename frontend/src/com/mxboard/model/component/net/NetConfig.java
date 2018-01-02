/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.net;

import java.util.HashMap;
import java.util.Set;

/**
 * <tt>NetConfig.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午9:36:50
 * @version 1.0
 */
public class NetConfig {
	private HashMap<String, String> netConfig = new HashMap<>();
	
	public NetConfig() {
		
	}
	
	public NetConfig add(String key, Object value) {
		netConfig.put(key, value.toString());
		return this;
	}
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		int size = netConfig.size();
		
		
		Set<String> keys = netConfig.keySet();
		
		int index = 0;
		for (String key : keys) {
			builder.append("\"")
					.append(key)
					.append("\": \"")
					.append(netConfig.get(key))
					.append("\"");
			if (index != size - 1) {
				builder.append(", ");
			}
			index++;
		}
		
		builder.append("}");
		
		return builder.toString();
	}
}
