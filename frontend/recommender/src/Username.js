import { Card, CardContent, Typography } from '@mui/material';
import React from 'react'

function Username(text, removeMember) {
    const ref = React.createRef() 

    const onMouseOver = () => {
        ref.current.style.textDecoration = "line-through"
    }

    const onMouseExit = () => {
        ref.current.style.textDecoration = "none"
    }

    return (
        <Card sx={{ minWidth: 275, padding: "1rem", marginLeft: "20rem", marginRight: "20rem"}} key={text} onClick={() => removeMember(text)}>
            <CardContent>
                <Typography ref={ref} sx={{ fontSize: 50, padding: "0.5rem", cursor: "grab"}} color="text.secondary" gutterBottom onMouseLeave={() => onMouseExit()} onMouseOver={() => onMouseOver()}>
                    {text}
                </Typography>
            </CardContent>
        </Card>
    )
}

export default Username;