/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.util;

import java.io.File;
import java.util.HashMap;
import java.util.List;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;

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
	
	private Element rootElement;
	
	public XMLConfigParser() {
		SAXReader saxReader = new SAXReader();
		try {
			Document document = saxReader.read(new File(XML_PATH));
			rootElement = document.getRootElement();
		} catch (DocumentException e) {
		}
	}
	
	public HashMap<String, String> getMongoConfig() {
		HashMap<String, String> mongoConfig = new HashMap<>();
		
		Element mongoConfElement = getSpecificElement("mongo-conf");
		@SuppressWarnings("unchecked")
		List<Element> elements = mongoConfElement.elements();
		for (Element element : elements) {
			String name = element.getName();
			String value = element.getText();
			mongoConfig.put(name, value);
		}
		
		return mongoConfig;
	}
	
	public HashMap<String, String> getGRpcConfig() {
		HashMap<String, String> gRpcConfig = new HashMap<>();
		
		Element gRpcConfigElement = getSpecificElement("rpc-conf");
		
		@SuppressWarnings("unchecked")
		List<Element> elements = gRpcConfigElement.elements();
		for (Element element : elements) {
			String name = element.getName();
			String value = element.getText();
			gRpcConfig.put(name, value);
		}
		
		return gRpcConfig;
	}
	
	private Element getSpecificElement(String elementName) {
		@SuppressWarnings("unchecked")
		List<Element> elements = rootElement.elements();
		for (Element element : elements) {
			if (element.getName().equals(elementName)) {
				return element;
			}
		}
		return null;
	}
}
