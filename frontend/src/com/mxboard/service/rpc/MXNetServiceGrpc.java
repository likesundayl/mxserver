package com.mxboard.service.rpc;

import static io.grpc.stub.ClientCalls.asyncUnaryCall;
import static io.grpc.stub.ClientCalls.asyncServerStreamingCall;
import static io.grpc.stub.ClientCalls.asyncClientStreamingCall;
import static io.grpc.stub.ClientCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ClientCalls.blockingUnaryCall;
import static io.grpc.stub.ClientCalls.blockingServerStreamingCall;
import static io.grpc.stub.ClientCalls.futureUnaryCall;
import static io.grpc.MethodDescriptor.generateFullMethodName;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedStreamingCall;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.0.0)",
    comments = "Source: mxboard.proto")
public class MXNetServiceGrpc {

  private MXNetServiceGrpc() {}

  public static final String SERVICE_NAME = "MXNetService";

  // Static method descriptors that strictly reflect the proto.
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<com.mxboard.service.rpc.Mxboard.SymbolParameter,
      com.mxboard.service.rpc.Mxboard.SymbolCreateState> METHOD_CREATE_SYMBOL =
      io.grpc.MethodDescriptor.create(
          io.grpc.MethodDescriptor.MethodType.UNARY,
          generateFullMethodName(
              "MXNetService", "createSymbol"),
          io.grpc.protobuf.ProtoUtils.marshaller(com.mxboard.service.rpc.Mxboard.SymbolParameter.getDefaultInstance()),
          io.grpc.protobuf.ProtoUtils.marshaller(com.mxboard.service.rpc.Mxboard.SymbolCreateState.getDefaultInstance()));
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<com.mxboard.service.rpc.Mxboard.TaskParameter,
      com.mxboard.service.rpc.Mxboard.TaskState> METHOD_START_TASK =
      io.grpc.MethodDescriptor.create(
          io.grpc.MethodDescriptor.MethodType.UNARY,
          generateFullMethodName(
              "MXNetService", "startTask"),
          io.grpc.protobuf.ProtoUtils.marshaller(com.mxboard.service.rpc.Mxboard.TaskParameter.getDefaultInstance()),
          io.grpc.protobuf.ProtoUtils.marshaller(com.mxboard.service.rpc.Mxboard.TaskState.getDefaultInstance()));
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<com.mxboard.service.rpc.Mxboard.TaskId,
      com.mxboard.service.rpc.Mxboard.TaskState> METHOD_STOP_TASK =
      io.grpc.MethodDescriptor.create(
          io.grpc.MethodDescriptor.MethodType.UNARY,
          generateFullMethodName(
              "MXNetService", "stopTask"),
          io.grpc.protobuf.ProtoUtils.marshaller(com.mxboard.service.rpc.Mxboard.TaskId.getDefaultInstance()),
          io.grpc.protobuf.ProtoUtils.marshaller(com.mxboard.service.rpc.Mxboard.TaskState.getDefaultInstance()));

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static MXNetServiceStub newStub(io.grpc.Channel channel) {
    return new MXNetServiceStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static MXNetServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new MXNetServiceBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary and streaming output calls on the service
   */
  public static MXNetServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new MXNetServiceFutureStub(channel);
  }

  /**
   */
  public static abstract class MXNetServiceImplBase implements io.grpc.BindableService {

    /**
     */
    public void createSymbol(com.mxboard.service.rpc.Mxboard.SymbolParameter request,
        io.grpc.stub.StreamObserver<com.mxboard.service.rpc.Mxboard.SymbolCreateState> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_CREATE_SYMBOL, responseObserver);
    }

    /**
     */
    public void startTask(com.mxboard.service.rpc.Mxboard.TaskParameter request,
        io.grpc.stub.StreamObserver<com.mxboard.service.rpc.Mxboard.TaskState> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_START_TASK, responseObserver);
    }

    /**
     */
    public void stopTask(com.mxboard.service.rpc.Mxboard.TaskId request,
        io.grpc.stub.StreamObserver<com.mxboard.service.rpc.Mxboard.TaskState> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_STOP_TASK, responseObserver);
    }

    @java.lang.Override public io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            METHOD_CREATE_SYMBOL,
            asyncUnaryCall(
              new MethodHandlers<
                com.mxboard.service.rpc.Mxboard.SymbolParameter,
                com.mxboard.service.rpc.Mxboard.SymbolCreateState>(
                  this, METHODID_CREATE_SYMBOL)))
          .addMethod(
            METHOD_START_TASK,
            asyncUnaryCall(
              new MethodHandlers<
                com.mxboard.service.rpc.Mxboard.TaskParameter,
                com.mxboard.service.rpc.Mxboard.TaskState>(
                  this, METHODID_START_TASK)))
          .addMethod(
            METHOD_STOP_TASK,
            asyncUnaryCall(
              new MethodHandlers<
                com.mxboard.service.rpc.Mxboard.TaskId,
                com.mxboard.service.rpc.Mxboard.TaskState>(
                  this, METHODID_STOP_TASK)))
          .build();
    }
  }

  /**
   */
  public static final class MXNetServiceStub extends io.grpc.stub.AbstractStub<MXNetServiceStub> {
    private MXNetServiceStub(io.grpc.Channel channel) {
      super(channel);
    }

    private MXNetServiceStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MXNetServiceStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new MXNetServiceStub(channel, callOptions);
    }

    /**
     */
    public void createSymbol(com.mxboard.service.rpc.Mxboard.SymbolParameter request,
        io.grpc.stub.StreamObserver<com.mxboard.service.rpc.Mxboard.SymbolCreateState> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_CREATE_SYMBOL, getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void startTask(com.mxboard.service.rpc.Mxboard.TaskParameter request,
        io.grpc.stub.StreamObserver<com.mxboard.service.rpc.Mxboard.TaskState> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_START_TASK, getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void stopTask(com.mxboard.service.rpc.Mxboard.TaskId request,
        io.grpc.stub.StreamObserver<com.mxboard.service.rpc.Mxboard.TaskState> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_STOP_TASK, getCallOptions()), request, responseObserver);
    }
  }

  /**
   */
  public static final class MXNetServiceBlockingStub extends io.grpc.stub.AbstractStub<MXNetServiceBlockingStub> {
    private MXNetServiceBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private MXNetServiceBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MXNetServiceBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new MXNetServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public com.mxboard.service.rpc.Mxboard.SymbolCreateState createSymbol(com.mxboard.service.rpc.Mxboard.SymbolParameter request) {
      return blockingUnaryCall(
          getChannel(), METHOD_CREATE_SYMBOL, getCallOptions(), request);
    }

    /**
     */
    public com.mxboard.service.rpc.Mxboard.TaskState startTask(com.mxboard.service.rpc.Mxboard.TaskParameter request) {
      return blockingUnaryCall(
          getChannel(), METHOD_START_TASK, getCallOptions(), request);
    }

    /**
     */
    public com.mxboard.service.rpc.Mxboard.TaskState stopTask(com.mxboard.service.rpc.Mxboard.TaskId request) {
      return blockingUnaryCall(
          getChannel(), METHOD_STOP_TASK, getCallOptions(), request);
    }
  }

  /**
   */
  public static final class MXNetServiceFutureStub extends io.grpc.stub.AbstractStub<MXNetServiceFutureStub> {
    private MXNetServiceFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private MXNetServiceFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MXNetServiceFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new MXNetServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.mxboard.service.rpc.Mxboard.SymbolCreateState> createSymbol(
        com.mxboard.service.rpc.Mxboard.SymbolParameter request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_CREATE_SYMBOL, getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.mxboard.service.rpc.Mxboard.TaskState> startTask(
        com.mxboard.service.rpc.Mxboard.TaskParameter request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_START_TASK, getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.mxboard.service.rpc.Mxboard.TaskState> stopTask(
        com.mxboard.service.rpc.Mxboard.TaskId request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_STOP_TASK, getCallOptions()), request);
    }
  }

  private static final int METHODID_CREATE_SYMBOL = 0;
  private static final int METHODID_START_TASK = 1;
  private static final int METHODID_STOP_TASK = 2;

  private static class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final MXNetServiceImplBase serviceImpl;
    private final int methodId;

    public MethodHandlers(MXNetServiceImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_CREATE_SYMBOL:
          serviceImpl.createSymbol((com.mxboard.service.rpc.Mxboard.SymbolParameter) request,
              (io.grpc.stub.StreamObserver<com.mxboard.service.rpc.Mxboard.SymbolCreateState>) responseObserver);
          break;
        case METHODID_START_TASK:
          serviceImpl.startTask((com.mxboard.service.rpc.Mxboard.TaskParameter) request,
              (io.grpc.stub.StreamObserver<com.mxboard.service.rpc.Mxboard.TaskState>) responseObserver);
          break;
        case METHODID_STOP_TASK:
          serviceImpl.stopTask((com.mxboard.service.rpc.Mxboard.TaskId) request,
              (io.grpc.stub.StreamObserver<com.mxboard.service.rpc.Mxboard.TaskState>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    return new io.grpc.ServiceDescriptor(SERVICE_NAME,
        METHOD_CREATE_SYMBOL,
        METHOD_START_TASK,
        METHOD_STOP_TASK);
  }

}
