/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component;

/**
 * <tt>Data.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午9:53:34
 * @version 1.0
 */
public class DataParam {
	private int batchSize = 32;
	private String name = "data";
	private int[] shapes;
	private String trainRecPath;
	private String valRecPath;
	
	public DataParam(int batchSize, String name, String trainRecPath, String valRecPath, int...shapes) {
		this.batchSize = batchSize > 0 ? batchSize : -batchSize;
		this.name = name;
		this.trainRecPath = trainRecPath;
		this.valRecPath = valRecPath;
		if (shapes.length == 0) {
			this.shapes = new int[] {1};
		} else {
			for(int shape : shapes) {
				if(shape == 0) {
					shape = 1;
				}
				shape = shape > 0 ? shape : -shape;
			}
			this.shapes = shapes;
		}
	}
	
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"batch_size\": \"")
				.append(batchSize).append("\", \"name\": \"")
				.append(name).append("\", \"shapes\": [");
		for (int i = 0 ; i < shapes.length ; i++) {
			builder.append("\"").append(shapes[i]).append("\"");
			if (i != shapes.length - 1) {
				builder.append(", ");
			}
		}
		builder.append("], \"file_path\": {\"train\": \"")
				.append(trainRecPath).append("\"");
		if(valRecPath == null) {
			builder.append("}}");
		} else {
			builder.append(", \"val\": \"")
					.append(valRecPath).append("\"}}");
		}
		
		return builder.toString();
	}
	
	public static void main(String[] args) {
		DataParam param = new DataParam(32, "data", "home/wuzhenan/train.rec", "home/wuzhenan/val.rec", 3, 128, 128);
		System.out.println(param.toJSON());
	}
}
