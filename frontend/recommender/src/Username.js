import { Button, Card, CardContent, Typography } from '@mui/material';
import { Box } from '@mui/system';
import React from 'react'

function Username(text, removeMember) {
    return (
        <Card sx={{ minWidth: 275, padding: "0.1rem", marginLeft: "20rem", marginRight: "20rem" }} key={text}>
            <CardContent>
                <Box sx={{ display: 'flex', flexDirection: "column" }}><Typography sx={{ fontSize: 35, padding: "0.5rem", cursor: "grab" }} color="text.secondary" gutterBottom>
                    {text}

                </Typography></Box>

                <Box sx={{ display: 'flex', flexDirection: "column" }}><Button x={{ marginLeft: 1000 }} onClick={() => removeMember(text)}> - </Button></Box>

            </CardContent>

        </Card >
    )
}

export default Username;