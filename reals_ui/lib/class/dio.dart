import 'package:json_annotation/json_annotation.dart';
part 'dio.g.dart';

@JsonSerializable()
class DioResponse {
  dynamic result;
  int status;
  String message;
  DioResponse(this.result, this.status, this.message);

  factory DioResponse.fromJson(Map<String, dynamic> json) =>
      _$DioResponseFromJson(json);

  Map<String, dynamic> toJson() => _$DioResponseToJson(this);
}
