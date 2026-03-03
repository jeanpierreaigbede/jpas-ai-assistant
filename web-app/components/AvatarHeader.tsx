import React from 'react'

type Props = {
  avatarUrl: string
  systemName: string
  description: string
}

export default function AvatarHeader({ avatarUrl, systemName, description }: Props) {
  return (
    <header className="header">
      <img src={avatarUrl} alt="avatar" className="avatar" />
      <div>
        <h1 className="title">{systemName}</h1>
        <p className="muted">{description}</p>
      </div>
    </header>
  )
}
