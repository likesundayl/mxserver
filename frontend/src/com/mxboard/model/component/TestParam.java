/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component;

/**
 * <tt>TestParam.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 下午3:42:59
 * @version 1.0
 */
public class TestParam {
	private CheckPointParam ckp;
	private String[] testImgs;
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"ckp\": ")
				.append(ckp.toJSON()).append(", \"test_imgs\": [");
		
		for(int i = 0 ; i < testImgs.length ; i++) {
			builder.append("\"").append(testImgs[i]).append("\"");
			if (i != testImgs.length - 1) {
				builder.append(", ");
			}
		}
		builder.append("]}");
		
		return builder.toString();
	}
}
