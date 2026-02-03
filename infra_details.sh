#!/bin/bash

KUBECONFIG=~/.kube/unified-demo

echo "Namespace,Workload,Type,Running Pods,Memory Usage,Memory Requests,Memory Requests %,Memory Limits,Memory Limits %"

# Get all running pods across namespaces
kubectl get pods -A --kubeconfig "$KUBECONFIG" -o json |
jq -r '
.items[]
| select(.status.phase=="Running")
| {
    ns: .metadata.namespace,
    pod: .metadata.name,
    kind: .metadata.ownerReferences[0].kind,
    owner: .metadata.ownerReferences[0].name,
    containers: .spec.containers
  }
| "\(.ns)|\(.owner)|\(.kind)|\(.containers | length)"
' |
sort | uniq | while IFS="|" read NS OWNER KIND CONTAINER_COUNT
do
  [ -z "$OWNER" ] && continue

  # -------------------------
  # Running Pods count
  # -------------------------
  POD_COUNT=$(kubectl get pods -n "$NS" --kubeconfig "$KUBECONFIG" \
    --field-selector=status.phase=Running \
    -o json |
    jq "[.items[] | select(.metadata.ownerReferences[0].name==\"$OWNER\")] | length")

  # -------------------------
  # Memory Usage (Mi)
  # -------------------------
  USAGE_MI=$(kubectl top pods -n "$NS" --kubeconfig "$KUBECONFIG" --no-headers 2>/dev/null |
    awk -v owner="$OWNER" '
    $1 ~ owner { gsub(/Mi/,"",$3); sum+=$3 }
    END { print sum+0 }')

  # -------------------------
  # Memory Requests / Limits
  # -------------------------
  REQ_MI=$(kubectl get pods -n "$NS" --kubeconfig "$KUBECONFIG" -o json |
    jq -r --arg owner "$OWNER" '
    [.items[]
     | select(.metadata.ownerReferences[0].name==$owner)
     | .spec.containers[].resources.requests.memory // "0Mi"]
    | map(
        if test("Gi") then (sub("Gi";"")|tonumber*1024)
        elif test("Mi") then (sub("Mi";"")|tonumber)
        else 0 end
      )
    | add')

  LIM_MI=$(kubectl get pods -n "$NS" --kubeconfig "$KUBECONFIG" -o json |
    jq -r --arg owner "$OWNER" '
    [.items[]
     | select(.metadata.ownerReferences[0].name==$owner)
     | .spec.containers[].resources.limits.memory // "0Mi"]
    | map(
        if test("Gi") then (sub("Gi";"")|tonumber*1024)
        elif test("Mi") then (sub("Mi";"")|tonumber)
        else 0 end
      )
    | add')

  # Convert to Gi
  USAGE_GI=$(echo "scale=2; $USAGE_MI/1024" | bc)
  REQ_GI=$(echo "scale=2; $REQ_MI/1024" | bc)
  LIM_GI=$(echo "scale=2; $LIM_MI/1024" | bc)

  # Percentages
  REQ_PCT=$( [ "$REQ_MI" -gt 0 ] && echo "scale=2; ($USAGE_MI/$REQ_MI)*100" | bc || echo "0" )
  LIM_PCT=$( [ "$LIM_MI" -gt 0 ] && echo "scale=2; ($USAGE_MI/$LIM_MI)*100" | bc || echo "0" )

  echo "$NS,$OWNER,${KIND:-pod},$POD_COUNT,${USAGE_GI} Gi,${REQ_GI} Gi,${REQ_PCT}%,${LIM_GI} Gi,${LIM_PCT}%"

done

