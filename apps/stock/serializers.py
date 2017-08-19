#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.account.models import Address
from apps.account.serializers import UserSerializer, AddressSerializer
from common.rest.serializers import ActiveModelSerializer, StatePrimaryKeyRelatedField
from . import models

User = get_user_model()


class WarehouseSerializer(ActiveModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    address_detail = AddressSerializer(source='address', read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True,profile__is_partner=True)
    )
    address = StatePrimaryKeyRelatedField(Address,'active')

    class Meta:
        model = models.Warehouse
        fields = ('name', 'user', 'address', 'user_detail', 'address_detail')


class ZoneSerializer(ActiveModelSerializer):
    warehouse = StatePrimaryKeyRelatedField(models.Warehouse, 'active')
    warehouse_detail = WarehouseSerializer(source='warehouse', read_only=True)

    class Meta:
        model = models.Zone
        fields = ('warehouse', 'usage', 'warehouse_detail')


class LocationSerializer(ActiveModelSerializer):
    index=serializers.ReadOnlyField()
    zone_detail = ZoneSerializer(source='zone', read_only=True)

    class Meta:
        model = models.Location
        fields = (
            'zone', 'parent_node', 'is_virtual',
            'x', 'y', 'z', 'zone_detail','index'
        )


class RouteSerializer(ActiveModelSerializer):
    warehouse = StatePrimaryKeyRelatedField(models.Warehouse, 'active')
    warehouse_detail=WarehouseSerializer(source='warehouse',read_only=True)
    zones_detail=ZoneSerializer(source='zones',many=True,read_only=True)
    class Meta:
        model= models.Route
        fields=(
            'name','warehouse','warehouse_detail',
            'zones_detail','sequence'
        )

class RouteZoneSettingSerializer(serializers.ModelSerializer):
    route = StatePrimaryKeyRelatedField(models.Route, 'active')
    zone = StatePrimaryKeyRelatedField(models.Zone, 'active')
    class Meta:
        model= models.RouteZoneSetting
        fields=(
            'route','zone','sequence'
        )

    def validate(self, attrs):
        route = attrs['route']
        zone = attrs['zone']
        if route.warehouse != zone.warehouse:
            raise serializers.ValidationError('区域所属的仓库必须与路线的仓库相同')
        return attrs

class PackageTypeItemSettingSerializer(serializers.ModelSerializer):
    package_type = StatePrimaryKeyRelatedField(models.PackageType, 'active')
    item = StatePrimaryKeyRelatedField(models.Item, 'active')
    class Meta:
        model= models.PackageTypeItemSetting
        fields=(
            'package_type','item','max_quantity'
        )

class PackageTypeSerializer(ActiveModelSerializer):
    class Meta:
        model= models.PackageType
        fields=('name','items')

class PackageTemplateItemSettingSerializer(serializers.ModelSerializer):
    package_template = StatePrimaryKeyRelatedField(models.PackageTemplate, 'active')
    type_setting_detail = PackageTypeItemSettingSerializer(
        source='type_setting',
        read_only=True,
        many=True
    )
    class Meta:
        model= models.PackageTemplateItemSetting
        fields=(
            'package_template','type_setting','quantity','type_setting_detail'
        )

class PackageTemplateSerializer(ActiveModelSerializer):
    package_type = StatePrimaryKeyRelatedField(models.PackageType, 'active')
    type_settings_detail=PackageTemplateItemSettingSerializer(
        source='type_settings',
        read_only=True,
        many=True
    )
    class Meta:
        model= models.PackageTemplate
        fields=(
            'name','package_type','type_settings','type_settings_detail'
        )

class PackageNodeSerializer(serializers.ModelSerializer):
    index=serializers.ReadOnlyField()
    template = StatePrimaryKeyRelatedField(models.PackageTemplate, 'active')
    template_detail=PackageTemplateSerializer(
        source='template',
        read_only=True
    )
    class Meta:
        model= models.PackageNode
        fields=(
            'name','parent_node','template','template_detail',
            'quantity','index'
        )

class ProcurementDetailSerializer(ActiveModelSerializer):
    from_location_detail = LocationSerializer(source='from_location',read_only=True)
    next_location_detail = LocationSerializer(source='next_location',read_only=True)
    item = StatePrimaryKeyRelatedField(models.Item,'active')
    class Meta:
        model= models.ProcurementDetail
        fields=(
            'from_location','next_location',
            'from_location_detail','next_location_detail',
            'item','quantity','procurement'
        )

class ProcurementSerializer(ActiveModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True,profile__is_partner=True)
    )
    user_detail=UserSerializer(source='user',read_only=True)
    route = StatePrimaryKeyRelatedField(models.Route, 'active')
    route_detail = RouteSerializer(source='route',read_only=True)
    class Meta:
        model= models.Procurement
        fields=(
            'user','user_detail','state','route','route_detail'
        )

class MoveSerializer(ActiveModelSerializer):
    from_zone_detail = ZoneSerializer(source='from_zone', read_only=True)
    to_zone_detail = ZoneSerializer(source='to_zone', read_only=True)
    to_moves = serializers.ReadOnlyField()
    procurement_details = ProcurementDetailSerializer(source='procurement_details',read_only=True,many=True)
    route_zone_setting = serializers.ReadOnlyField()
    quantity = serializers.ReadOnlyField()
    state = serializers.CharField(read_only=True)

    class Meta:
        model = models.Move
        fields = (
            'from_zone_detail',
            'to_zone_detail','item',
            'to_moves', 'procurement_details',
            'route_zone_setting','quantity', 'state'
        )