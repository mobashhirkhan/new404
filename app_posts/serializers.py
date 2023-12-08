from rest_framework import serializers

from base.forms import toCommonMark

from .models import AppPost


class AppPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPost
        fields = [
            "type",
            "id",
            "author",
            "title",
            "description",
            "source",
            "origin",
            "contentType",
            "content",
            "image",
            "count",
            "published",
            "visibility",
            "unlisted",
            "liked",
            "comments",
        ]
        read_only_fields = [
            "type",
            "id",
            "source",
            "origin",
            "count",
            "published",
            "liked",
            "comments",
        ]

    def create(self, validated_data):
        # print("creating?")
        """
        Create and return new AppPost instance given validated data
        """
        initial_content = validated_data.get("content")

        # take user input and set plain and markdown directly, dont change user initial content
        md_content = toCommonMark(initial_content)
        validated_data["contentPlain"] = initial_content
        validated_data["contentMarkdown"] = md_content

        # set source and origin

        # set comment count

        # set unlisted

        # set liked

        new_part_instance = AppPost.objects.create(**validated_data)

        return new_part_instance

    def update(self, instance, validated_data):
        # print("updating?")
        """
        Update and return an existing `AppPost` instance, given the validated data
        """

        if self.partial:
            # needs to be manual i guess
            if "title" in validated_data:
                instance.title = validated_data.get("title", instance.title)
            if "description" in validated_data:
                instance.description = validated_data.get(
                    "description", instance.description
                )
            if "contentType" in validated_data:
                instance.contentType = validated_data.get(
                    "contentType", instance.contentType
                )
            if "content" in validated_data:
                initial_content = validated_data.get("content")
                instance.contentPlain = initial_content
                instance.contentMarkdown = toCommonMark(initial_content)
                instance.content = initial_content
            if "categories" in validated_data:
                instance.categories = validated_data.get(
                    "categories", instance.categories
                )
            if "visibility" in validated_data:
                instance.visibility = validated_data.get(
                    "visibility", instance.visibility
                )

        else:
            # set content types
            # get initial user input. needed because will need to display back tpo usern their input
            initial_content = validated_data.get("content")
            # take user input and set plain and markdown directly, dont change user initial content
            md_content = toCommonMark(initial_content)

            print("deep ends")
            print(validated_data)

            # set source and origin

            # set comment count

            # set unlisted

            # set liked

            # set all fields
            instance.contentPlain = initial_content
            instance.contentMarkdown = md_content

            instance.author = validated_data.get("author", instance.author)
            instance.title = validated_data.get("title", instance.title)
            instance.description = validated_data.get(
                "description", instance.description
            )
            instance.contentType = validated_data.get(
                "contentType", instance.contentType
            )
            instance.content = validated_data.get("content", instance.content)
            instance.categories = validated_data.get("categories", instance.categories)
            instance.visibility = validated_data.get("visibility", instance.visibility)

        instance.save()
        return instance
