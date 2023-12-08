from rest_framework import serializers

from base.forms import toCommonMark

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "type",
            "origin",
            "summary",
            "author",
            "contentType",
            "content",
            "contentPlain",
            "contentMarkdown",
            "published",
            "post",
            "liked",
        ]
        read_only_fields = [
            "id",
            "type",
            "origin",
            "summary",
            "contentPlain",
            "contentMarkdown",
            "published",
            "post",
            "liked",
        ]

    def create(self, validated_data):
        """
        Create and return new Comment instance given validated data
        """
        print("creating?")
        initial_content = validated_data.get("content")
        
        # take user input and set plain and markdown directly, dont change user initial content
        md_content = toCommonMark(initial_content)
        validated_data["contentPlain"] = initial_content
        validated_data["contentMarkdown"] = md_content

        # set unlisted

        # set liked

        new_comment_instance = Comment.objects.create(**validated_data)

        return new_comment_instance

    def update(self, instance, validated_data):
        # print("updating?")
        """
        Update and return an existing `AppPost` instance, given the validated data
        """

        if self.partial:
            # needs to be manual i guess

            if "contentType" in validated_data:
                instance.contentType = validated_data.get(
                    "contentType", instance.contentType
                )
            if "content" in validated_data:
                initial_content = validated_data.get("content")
                instance.contentPlain = initial_content
                instance.contentMarkdown = toCommonMark(initial_content)
                instance.content = initial_content

        else:
            # set content types
            # get initial user input. needed because will need to display back tpo usern their input
            initial_content = validated_data.get("content")
            # take user input and set plain and markdown directly, dont change user initial content
            md_content = toCommonMark(initial_content)

            print("deep ends comments")
            # print(instance)
            # print(validated_data)

            # set all relevant fields
            instance.contentPlain = initial_content
            instance.contentMarkdown = md_content

            instance.contentType = validated_data.get(
                "contentType", instance.contentType
            )
            instance.content = validated_data.get("content", instance.content)

        instance.save()
        return instance
