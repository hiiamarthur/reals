// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'dio.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

DioResponse _$DioResponseFromJson(Map<String, dynamic> json) => DioResponse(
      json['result'],
      (json['status'] as num).toInt(),
      json['message'] as String,
    );

Map<String, dynamic> _$DioResponseToJson(DioResponse instance) =>
    <String, dynamic>{
      'result': instance.result,
      'status': instance.status,
      'message': instance.message,
    };
