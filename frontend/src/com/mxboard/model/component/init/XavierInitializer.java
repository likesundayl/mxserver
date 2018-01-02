/**
 * Copyright (c) 2017 Terence Wu
 */
package com.mxboard.model.component.init;

/**
 * <tt>XaiverInitializer.java</tt><br>
 * 
 * @author TerenceWu
 * @time 2018年1月2日 上午11:10:24
 * @version 1.0
 */
public class XavierInitializer extends Initializer {
	private String rndType = "uniform";
	private String factorType = "avg";
	private float magnitude = 3;
	
	public XavierInitializer(float manitude) {
		this.type = "Xavier";
		this.magnitude = manitude > 0 ? manitude : -manitude;
	}
	
	public XavierInitializer(String rndType, String factorType, float manitude) {
		this.type = "Xavier";
		this.rndType = rndType;
		this.factorType = factorType;
		this.magnitude = manitude > 0 ? manitude : -manitude;
	}
	
	@Override
	public String toJSON() {
		StringBuilder builder = new StringBuilder("{");
		
		builder.append("\"type\": \"")
				.append(type).append("\", \"init_config\": {")
				.append("\"rnd_type\": \"")
				.append(rndType).append("\", \"factor_type\": \"")
				.append(factorType).append("\", \"magnitude\": \"")
				.append(magnitude).append("\"}}");
		
		return builder.toString();
	}
}
