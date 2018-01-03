/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.net;

/**
 * <tt>Symbol.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午9:59:57
 * @version 1.0
 */
public class Symbol {
	private String name;
	
	public Symbol(String name) {
		this.name = name;
	}
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"name\": \"").append(name).append("\"}");
		
		return builder.toString();
	}
	
	public static void main(String[] args) {
		Symbol symbol = new Symbol("AlexNet");
		System.out.println(symbol.toJSON());
	}
}
