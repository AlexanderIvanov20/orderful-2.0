from typing import Any

from fastapi import HTTPException, status

from orderful.services.base import BaseService, CreateSchemaType, ModelType, UpdateSchemaType


class AssociationsMixin:
    @staticmethod
    def _extract_associations_from_data(
        data: CreateSchemaType, associated_field: str
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        data_dump = data.model_dump(exclude_unset=True)
        return data_dump, data_dump.pop(associated_field)

    @staticmethod
    def _extract_ids_from_associations(associated_id: int, associations: list[dict[str, Any]]) -> list[int]:
        return [association[associated_id] for association in associations]

    @staticmethod
    def _get_associated_instances_by_ids(
        association_ids: list[int], associated_service: BaseService
    ) -> list[ModelType]:
        return associated_service.filter(associated_service.model.id.in_(association_ids)).all()

    @staticmethod
    def _validate_associated_instances_existence(
        associated_field: str, associated_ids: list[int], associated_instances: list[ModelType]
    ) -> None:
        if non_existing_ids := set(associated_ids) - {instance.id for instance in associated_instances}:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The {associated_field} with the IDs={non_existing_ids} do(es) not exist.",
            )

    @staticmethod
    def _prepare_association_instance(
        association: dict[str, Any],
        association_model: type[ModelType],
        instance_name: str,
        instance: ModelType,
    ) -> dict[str, Any]:
        association[instance_name] = instance
        return association_model(**association)

    @staticmethod
    def _validate(
        associations_data: list[dict[str, Any]],
        association_ids: list[int],
        associated_instances: list[ModelType],
    ) -> None:
        pass

    def _set_associations_for_instance(
        self,
        instance: ModelType,
        instance_name: str,
        associated_field: str,
        association_model: type[ModelType],
        associations_data: list[dict[str, Any]],
    ) -> None:
        associations_instances = [
            self._prepare_association_instance(association, association_model, instance_name, instance)
            for association in associations_data
        ]
        setattr(instance, associated_field, associations_instances)

        self.session.add(instance)
        self.session.commit()

    def save_with_associations(
        self,
        data: CreateSchemaType | UpdateSchemaType,
        associated_id: int,
        associated_field: str,
        instance_name: str,
        associated_service: BaseService,
        association_model: ModelType,
        instance: ModelType = None,
        **kwargs: Any,
    ):
        data, associations_data = self._extract_associations_from_data(data, associated_field)
        association_ids = self._extract_ids_from_associations(associated_id, associations_data)
        associated_instances = self._get_associated_instances_by_ids(association_ids, associated_service)

        self._validate_associated_instances_existence(associated_field, association_ids, associated_instances)
        self._validate(associations_data, associated_instances)

        if not instance:
            instance = super().create(data, **kwargs)
        else:
            instance = self.update(instance, data, **kwargs)

        self._set_associations_for_instance(
            instance, instance_name, associated_field, association_model, associations_data
        )

        return instance
