/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.db;

import java.util.HashMap;

import com.mongodb.MongoClient;
import com.mxboard.util.XMLConfigParser;

/**
 * <tt>MongoConnector.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2017年12月25日 下午5:07:46
 * @version 1.0
 */
public class MongoConnector {
	private static HashMap<String, String> mongoConfig = (new XMLConfigParser()).getMongoConfig();
	private MongoClient client;
	public MongoConnector() {
		
	}
	
	public String queryTaskProgress(String taskId) {
		return "";
	}
}
