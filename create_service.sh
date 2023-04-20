output=$(clearml-serving create --name "${service_name}" --project "${service_project}")
service_id=$(echo "$output" | grep -oP 'id=\K[a-z0-9]+')
echo "#{setValue(service_id=${service_id})}"
