/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.util;

/**
 * <tt>XMLConfigParser.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2017年12月25日 上午9:10:53
 * @version 1.0
 */
public class XMLConfigParser {
	private static final String FILE_SEP = System.getProperty("file.separator");
	private static final String FOLDER_NAME = "conf";
	private static final String XML_NAME = "mxboard.xml";
	private static String XML_PATH = System.getProperty("user.dir");
	
	static {
		int lastSepIndex = XML_PATH.lastIndexOf(FILE_SEP);
		XML_PATH = XML_PATH.substring(0, lastSepIndex + 1) + FOLDER_NAME + FILE_SEP + XML_NAME;
	}
}
