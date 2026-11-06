export function subjectBreadcrumbs(subject) {
  if (!subject) return [{ label: 'Institutionen', to: '/' }]
  return [
    { label: 'Institutionen', to: '/' },
    { label: subject.institution.name, to: `/institutions/${subject.institution.uuid}` },
    { label: subject.name, to: `/subjects/${subject.uuid}` },
  ]
}

export function learningSetBreadcrumbs(learningSet, label) {
  const crumbs = subjectBreadcrumbs(learningSet?.subject)
  if (!label) return [...crumbs, { label: learningSet?.title ?? '' }]
  return [
    ...crumbs,
    { label: learningSet?.title ?? '', to: learningSet && `/learning-sets/${learningSet.uuid}` },
    { label },
  ]
}
