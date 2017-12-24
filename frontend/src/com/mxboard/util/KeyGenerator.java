/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.util;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * <tt>KeyGenerator.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2017年12月24日 下午10:27:44
 * @version 1.0
 */
public class KeyGenerator {
	private static final SimpleDateFormat DATE_FORMAT = new SimpleDateFormat("yyyyMMddHHmmss");
	
	public String generateKey() {
		String key = "";
		String time = DATE_FORMAT.format(new Date());
		key += time;
		// TODO:
		
		return key;
	}
}
