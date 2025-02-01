from rest_framework import serializers
from .models import Pegawai


class PegawaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pegawai
        fields = '__all__'

class PegawaiUploadCSVSerializer(serializers.Serializer):
    file = serializers.FileField()


    def validate_file(self, value):
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError("extensi file tidak dizinkan, upload file csv")

        try:
            file_content = value.read().decode("utf-8")  # Read & decode file content
            value.seek(0)  # Reset file pointer after reading

            # Ensure the first row contains CSV headers (e.g., "nip,nama,jabatan,grade")
            first_line = file_content.splitlines()[0]
            required_headers = {"nip", "nama", "jabatan", "grade"}
            if not required_headers.issubset(set(first_line.split(","))):
                raise serializers.ValidationError("Invalid CSV format or missing headers.")

        except Exception:
            raise serializers.ValidationError("Invalid CSV file content.")

        return value
