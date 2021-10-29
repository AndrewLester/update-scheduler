import moment from 'moment';

export interface ScheduledJob {
    id: string;
    scheduled_at?: string;
    scheduled_for?: string;
    scheduled_in?: string;
}

export interface Attachment {
    id: number;
    type: 'file' | 'link' | 'video';
    title?: string;
    url: string;
    image?: string;
    icon?: string;
    summary?: string;
}

export interface Update {
    id: number;
    body: string;
    job: ScheduledJob | null;
    attachments: Attachment[];
    realms: Realm[];
}

export interface Realm {
    id: string;
    name: string;
    type: string;
}

export function isScheduled(update: Update): boolean {
    return update.job !== null && update.job.id !== '';
}

const schoologyTimestampFormat = 'YYYY-MM-DD HH:mm:ss';

export function schoologyTimeToMoment(
    schoologyTimestamp: string
): moment.Moment {
    return moment(schoologyTimestamp, schoologyTimestampFormat);
}

export function momentToSchoologyTime(momentInstance: moment.Moment): string {
    return momentInstance.format(schoologyTimestampFormat);
}

export function getNewUpdate(): Update {
    return {
        id: -1,
        body: '',
        attachments: [],
        realms: [],
        job: null,
    };
}
