SELECT id
FROM {{ ref('users') }}
WHERE id IS NOT NULL
GROUP BY id
HAVING COUNT(*) > 1
